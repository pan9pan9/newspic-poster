import requests

class ThreadsAPI:
    def __init__(self, access_token: str, user_id: str):
        self.access_token = access_token
        self.user_id = user_id

    def create_media(self, media_type: str, **kwargs):
        """
        Threads 미디어 컨테이너 생성
        :param media_type: 'IMAGE' or 'TEXT'
        :param kwargs: image_url, text 등 추가 파라미터
        :return: response dict
        """
        url = f"https://graph.threads.net/v1.0/{self.user_id}/threads"
        params = {"media_type": media_type, "access_token": self.access_token, **kwargs}
        response = requests.post(url, data=params).json()
        print(f"✅ create_media 응답: {response}")
        return response

    def publish_media(self, creation_id: str):
        """
        생성한 미디어 컨테이너 발행
        :param creation_id: 미디어 컨테이너 ID
        :return: response dict
        """
        url = f"https://graph.threads.net/v1.0/{self.user_id}/threads_publish"
        params = {"creation_id": creation_id, "access_token": self.access_token}
        response = requests.post(url, data=params).json()
        print(f"✅ publish_media 응답: {response}")
        return response

    def reply_to_post(self, parent_id: str, text: str):
        """
        특정 게시물에 댓글(텍스트) 달기
        :param parent_id: 원본 포스트 ID
        :param text: 댓글 내용
        :return: response dict
        """
        url = f"https://graph.threads.net/v1.0/me/threads"
        params = {
            "media_type": "TEXT",
            "text": text,
            "reply_to_id": parent_id,
            "access_token": self.access_token
        }
        response = requests.post(url, data=params).json()
        print(f"✅ reply_to_post 응답: {response}")
        return response