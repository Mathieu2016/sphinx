import whisper


def transcribe(record_filename: str, model: str) -> str:
    model = whisper.load_model(model)

    return model.transcribe(record_filename, language='Chinese')['text']


if __name__ == '__main__':
    transcribe('temp/data_vally.m4a', 'small')
