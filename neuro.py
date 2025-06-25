from yandex_cloud_ml_sdk import YCloudML
from config import API, FOLDER

sdk = YCloudML(
    folder_id=FOLDER,
    auth=API
)
model = sdk.models.completions("yandexgpt")


async def neuroset(promt):
    result = model.run(promt)
    return str(result.alternatives[0].text)
