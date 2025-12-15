import soundfile as sf


ALLOWED_SAMPLE_RATES = {44100, 48000, 96000}


def validate_audio(file_path, expect_stereo=None):
    """
    Returns a list of validation issues (empty list = valid)
    """
    issues = []

    try:
        info = sf.info(file_path)
    except Exception as e:
        return [f"Could not read audio file: {e}"]

    # Sample rate check
    if info.samplerate not in ALLOWED_SAMPLE_RATES:
        issues.append(f"Invalid sample rate: {info.samplerate} Hz")

    # Channel count check
    if expect_stereo is True and info.channels != 2:
        issues.append("Expected stereo file")
    elif expect_stereo is False and info.channels != 1:
        issues.append("Expected mono file")

    return issues
