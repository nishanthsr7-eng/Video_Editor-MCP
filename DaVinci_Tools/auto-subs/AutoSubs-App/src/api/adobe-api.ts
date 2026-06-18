import { invoke } from '@tauri-apps/api/core';

export async function sendToAdobe(type: string, payload: any = {}, sessionId?: string, integration?: string) {
  const finalSessionId = sessionId || `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
  await invoke<string>('send_to_adobe', {
    payload: {
      type,
      payload,
      sessionId: finalSessionId,
    },
    integration,
  });
  return finalSessionId;
}

export async function requestSequenceInfo(sessionId?: string, integration?: string) {
  return sendToAdobe('request_sequence_info', {}, sessionId, integration);
}

export async function requestAudioExport(
  exportFolder: string,
  selectedTracks: number[],
  selectedRange: string = 'entire',
  presetPath: string = '',
  sessionId?: string,
  integration?: string
) {
  return sendToAdobe(
    'request_audio_export',
    { exportFolder, selectedTracks, selectedRange, presetPath },
    sessionId,
    integration
  );
}

export async function requestImportSRT(filePath: string, sessionId?: string, integration?: string) {
  return sendToAdobe('request_import_srt', { filePath }, sessionId, integration);
}

export async function requestJumpToTime(seconds: number, sessionId?: string, integration?: string) {
  return sendToAdobe('request_jump_to_time', { time: seconds }, sessionId, integration);
}
