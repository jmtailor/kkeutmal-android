package com.kkeutmal.app;

import android.content.Context;
import android.media.AudioAttributes;
import android.media.AudioFocusRequest;
import android.media.AudioManager;
import android.os.Build;

import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/** Takes / releases Android audio focus so other apps' media playback pauses while the game is used. */
@CapacitorPlugin(name = "AudioFocus")
public class AudioFocusPlugin extends Plugin {
    private AudioFocusRequest request; // API 26+
    private final AudioManager.OnAudioFocusChangeListener listener = change -> { };

    private AudioManager am() {
        return (AudioManager) getContext().getSystemService(Context.AUDIO_SERVICE);
    }

    @PluginMethod
    public void request(PluginCall call) {
        AudioManager am = am();
        int result;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            if (request == null) {
                AudioAttributes attrs = new AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_MEDIA)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                        .build();
                request = new AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN)
                        .setAudioAttributes(attrs)
                        .setOnAudioFocusChangeListener(listener)
                        .build();
            }
            result = am.requestAudioFocus(request);
        } else {
            result = am.requestAudioFocus(listener, AudioManager.STREAM_MUSIC, AudioManager.AUDIOFOCUS_GAIN);
        }
        call.resolve();
    }

    @PluginMethod
    public void abandon(PluginCall call) {
        AudioManager am = am();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            if (request != null) am.abandonAudioFocusRequest(request);
        } else {
            am.abandonAudioFocus(listener);
        }
        call.resolve();
    }
}
