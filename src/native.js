// Bundled into www/native.js. Exposes the Capacitor plugins to the game page.
import { Capacitor, registerPlugin } from '@capacitor/core';
import { SpeechRecognition } from '@capacitor-community/speech-recognition';
import { TextToSpeech } from '@capacitor-community/text-to-speech';

if (Capacitor.isNativePlatform()) {
  // AudioFocus: local Android plugin (AudioFocusPlugin.java) that stops other apps' media.
  const AudioFocus = registerPlugin('AudioFocus');
  window.KK_NATIVE = { SpeechRecognition, TextToSpeech, AudioFocus };
}
