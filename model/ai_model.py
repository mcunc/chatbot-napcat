import toml
from model.logger import setup_logger


logger = setup_logger()
def main(message,qid,group_openid):

        with open('./config.toml', 'r', encoding='utf-8') as f:
            config = toml.load(f)
            ai_service = config.get("ai_service")
            enable_qid = config.get("enable_qid")
            qid_prefix = config.get("qid_prefix")
            qid_suffix = config.get("qid_suffix")
            error_message = config.get("error_message")

        if enable_qid:
            message = f"{qid_prefix}{qid}{qid_suffix}{message}"
        else:
            pass

        if ai_service == "dify":
            from model.ai_models import dify
            return dify.main(message, group_openid)
        elif ai_service == "mcunc":
            from model.ai_models import mcunc
            return mcunc.main(message, group_openid)
        elif ai_service == "xyit":
            from model.ai_models import xyit
            return xyit.main(message, group_openid)
        else:
            logger.error("未配置ai_service")
            return error_message



