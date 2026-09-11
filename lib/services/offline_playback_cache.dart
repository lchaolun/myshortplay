import '../models/episode.dart';
import 'download_service.dart';
import 'video_save_service.dart';

class OfflinePlaybackCache {
  static Future<List<Episode>> completedEpisodesFromGroup(
    DramaDownloadGroup group,
  ) async {
    final completed = <Episode>[];
    for (final episode in group.episodes) {
      final path = episode.localPath;
      if (episode.status != DownloadStatus.completed || path == null) {
        continue;
      }
      if (!await VideoSaveService.isPublishedFileAvailable(path)) continue;
      completed.add(
        Episode(
          index: episode.episode.index,
          name: episode.episode.name,
          size: episode.episode.size,
          url: path,
        ),
      );
    }
    completed.sort((a, b) => a.index.compareTo(b.index));
    return completed;
  }
}
