import pandas as pd
import os
import pickle
from videotrackersystem.core import get_current_dir
from videotrackersystem.core import logger


def export_xlsx(fp_xlsx):
    try:
        with open(os.path.join(get_current_dir(), ".tmp-task.txt"), "rb") as f:
                ret = pickle.loads(f.read())
        
        dfs = {}
        for p, v in ret.items():
            _, fn = os.path.split(p)
            nv = [{"序号": _v[0], "内容": _v[1]} for _v in v]
            dfs[fn] = pd.DataFrame(nv)
        
        with pd.ExcelWriter(fp_xlsx, engine='xlsxwriter') as writer:
            for fn, vdf in dfs.items():
                vdf.to_excel(writer, index=False, sheet_name=fn)

        logger.info(f"save the xlsx file: {fp_xlsx}")
        return True
    except:
         logger.exception(f"save excel error")
         return False
