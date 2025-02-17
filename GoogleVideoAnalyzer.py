import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), "Keys", "GoogleKey.json")
from google.cloud import videointelligence

class GoogleVideoAnalyzer:
    def analyze_video_labels(self,video_uri):
        """Analyzes a video and extracts labels."""
        client = videointelligence.VideoIntelligenceServiceClient()

        features = [videointelligence.Feature.LABEL_DETECTION]
        operation = client.annotate_video(input_uri=video_uri, features=features)

        print("Processing video...")
        result = operation.result(timeout=300)

        labels = []
        for annotation in result.annotation_results[0].segment_label_annotations:
            label = annotation.entity.description
            labels.append(label)
    
        return labels




