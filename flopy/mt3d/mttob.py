from ..pakbase import Package


class Mt3dTob(Package):
    '''
    Transport Observation package class
    '''

    def __init__(self, model, outnam='tob_output', CScale=1.0, FluxGroups=[],
                 FScale=1.0, iOutFlux=0, extension='tob', unitnumber=None,
                 filenames=None):

        if unitnumber is None:
            unitnumber = Mt3dTob.defaultunit()
        elif unitnumber == 0:
            unitnumber = Mt3dTob.reservedunit()

        # set filenames
        if filenames is None:
            filenames = [None]
        elif isinstance(filenames, str):
            filenames = [filenames]

        # Fill namefile items
        name = [Mt3dTob.ftype()]
        units = [unitnumber]
        extra = ['']

        # set package name
        fname = [filenames[0]]

        # Call ancestor's init to set self.parent, extension, name and unit number
        Package.__init__(self, model, extension=extension, name=name,
                         unit_number=units, extra=extra, filenames=fname)

        self.heading = '# TOB for MT3DMS, generated by Flopy.'
        self.outnam = outnam
        self.CScale = CScale
        self.FluxGroups = FluxGroups
        self.FScale = FScale
        self.iOutFlux = iOutFlux
        self.parent.add_package(self)
        return

    def __repr__(self):
        return 'Transport Observation package class'

    def write_file(self):
        """
        Write the package file

        Returns
        -------
        None

        """
        # Open file for writing
        f_tob = open(self.fn_path, 'w')
        f_tob.write('%s\n' % (self.heading))
        MaxConcObs = 0
        MaxFluxObs = 0
        MaxFluxCells = 0
        inConcObs = 0
        inFluxObs = 88
        inSaveObs = 89
        if (inFluxObs):
            for FluxGroup in self.FluxGroups:
                MaxFluxCells = MaxFluxCells + len(FluxGroup[1])
                MaxFluxObs = MaxFluxObs + 1
        f_tob.write('%10d%10d%10d\n' % (MaxConcObs, MaxFluxObs, MaxFluxCells))
        f_tob.write('%s%10d%10d%10d\n' % (self.outnam, inConcObs, inFluxObs,
                                          inSaveObs))
        # if (inConcObs):
        #
        if (inFluxObs):
            nFluxGroup = len(self.FluxGroups)
            f_tob.write('%10d%10f%10d\n' % (nFluxGroup, self.FScale,
                                            self.iOutFlux))
            for FluxGroup in self.FluxGroups:
                nFluxTimeObs, FluxTimeObs = (
                    self.assign_layer_row_column_data(FluxGroup[0], 5,
                                                      zerobase=False))  # misuse of function - zerobase set to False
                nCells, Cells = self.assign_layer_row_column_data(FluxGroup[1],
                                                                  4,
                                                                  zerobase=False)  # misuse of function - zerobase set to False
                nCells = 4
                iSSType = FluxGroup[2]
                f_tob.write('%10d%10d%10d\n' % (nFluxTimeObs, nCells, iSSType))
                for fto in FluxTimeObs:
                    fto = fto[0]  # Still to fix this!
                    f_tob.write('%12s%10s%10s%10s%10s\n' % (fto[0], fto[1],
                                                            fto[2], fto[3],
                                                            fto[4]))
                for c in Cells:
                    c = c[0]  # Still to fix this!
                    f_tob.write('%10d%10d%10d%10f\n' % (c[0], c[1], c[2],
                                                        c[3]))

        f_tob.close()
        return

    @staticmethod
    def ftype():
        return 'TOB'

    @staticmethod
    def defaultunit():
        return 37

    @staticmethod
    def reservedunit():
        return 12
