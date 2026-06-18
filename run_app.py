import argparse
import json

from src.inference.predictor import predict_fake_news


def main():
    parser = argparse.ArgumentParser(description="Anti fake news multimodal detector")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--text", required=True, help="Vietnamese post title/content")
    args = parser.parse_args()

    result = predict_fake_news(args.image, args.text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

