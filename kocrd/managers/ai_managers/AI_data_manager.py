# AI_data_manager.py
import logging
from datetime import datetime
from PyQt5.QtWidgets import QInputDialog # UI 관련 import 는 이 파일에서 제거

class AIDataManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def save_feedback(self, data):
        """피드백 데이터 저장."""
        try:
            self.database_manager.save_feedback(data)
            logging.info(f"피드백 저장 완료: {data}")
        except Exception as e:
            logging.exception(f"피드백 저장 오류: {e}") # logging.exception 사용, 예외 다시 발생시키지 않음

    def request_user_feedback(self, file_path):
        """사용자 피드백 요청. UI 로직은 이 함수에 남겨둠."""
        valid_doc_types = self.database_manager.get_valid_doc_types()
        doc_type, ok = QInputDialog.getItem(
            None, '문서 유형 확인', f'문서 "{file_path}"의 유형을 선택해주세요:', valid_doc_types, 0, False
        )
        if ok and doc_type:
            try: # save_feedback에서 발생할 수 있는 예외를 여기서 처리
                self.save_feedback({
                    'file_path': file_path,
                    'doc_type': doc_type,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                return doc_type
            except Exception as e:
                logging.exception(f"피드백 저장 후 오류 발생: {e}")
                # 필요한 경우 QMessageBox를 여기서 다시 표시
                from PyQt5.QtWidgets import QMessageBox # QMessageBox import를 try 블록 안으로 옮김
                QMessageBox.critical(None, "오류", f"피드백 저장 후 오류가 발생했습니다: {e}")
                return None
        return None