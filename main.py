from email.mime import audio
import speech_recognition as sr

if __name__ == '__main__':

  def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
      
      raise TypeError('"recognizer" must be "Recognizer" instance')

    if not isinstance(microphone, sr.Microphone):

      raise TypeError('"microphone" must be "Microphone" instance')
    
    with microphone as src:
      recognizer.adjust_for_ambient_noise(src)
      audio = recognizer.listen(src)

    response = {
      'success': True,
      'error': None,
      'transcription': None,
    }

    try:
      response['transcription'] = recognizer.recognize_google(audio, language='ru-RU')
    except sr.RequestError: 

      response['success'], response['error'] = False, 'Unavailable API'

    except sr.UnknownValueError:

      response['error'] = 'Unable to recognize speech'

    return response
    

  recognizer = sr.Recognizer()
  mic = sr.Microphone(device_index = 1)
  response = recognize_speech_from_mic(recognizer, mic)
  print('\nSuccess : {}\nError   : {}\n\nText from Speech\n{}\n\n{}' \
          .format(response['success'],
                  response['error'],
                  '-'*17,
                  response['transcription']))