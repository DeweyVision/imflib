from imflib import cpl, opl, pkl, assetmap
import pathlib, typing, dataclasses


@dataclasses.dataclass
class Imf:
    """An IMF package"""
    asset_map:assetmap.AssetMap
    cpls:typing.List[cpl.Cpl]
    pkls:typing.List[pkl.Pkl]
    opls:typing.Optional = None

    @classmethod
    def from_path(cls, path_imf:typing.Union[str,pathlib.Path]) -> "Imf":
        """Parse an existing IMF"""
        
        path_imf = pathlib.Path(path_imf)
        if not path_imf.is_dir():
            raise NotADirectoryError(f"Path does not exist or is not a directory: {path_imf}")
        
        input_assetmap = assetmap.AssetMap.from_file(pathlib.Path(path_imf,"ASSETMAP.xml"))
        
        glob_temp = list(path_imf.glob("PKL*.xml"))
        if not len(glob_temp):
            raise FileNotFoundError(f"Could not find any PKLs in this directory")

        input_pkls = [
            pkl.Pkl.from_file(pkl_path)
            for pkl_path in glob_temp
        ]

        glob_temp = list(path_imf.glob("CPL*.xml"))
        if not len(glob_temp):
            raise FileNotFoundError("Could not find a CPL in this directory")

        input_cpls = [
            cpl.Cpl.from_file(path_cpl)
            for path_cpl in glob_temp
        ]
        
        # Marry the pkl assets to the CPL
        # BROKEN: I don't remember what I did here before.
        # TODO: Remember what I did there before.
        #for res in input_cpl.resources:
        #    res.setAsset(input_pkl.get_asset(res.file_id))

        glob_temp = list(path_imf.glob("OPL*.xml"))
        if glob_temp:
            input_opls = [
                opl.Opl.from_file(path_opl)
                for path_opl in glob_temp
            ]
        else:
            input_opls = None
        
        return cls(input_assetmap, input_cpls, input_pkls, input_opls)
