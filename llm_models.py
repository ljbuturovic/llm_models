#!/usr/bin/env python3
"""Quick script to list available LLM models from various providers"""

import argparse
import os
import sys

parser = argparse.ArgumentParser(description="List available LLM models from various providers")
parser.add_argument("--provider",
                    required=True,
                    choices=["OpenAI", "Google", "Anthropic", "xAI"],
                    help="LLM provider to query")
parser.add_argument("--region",
                    help="Region to use with Google Vertex AI API (requires --vertexai)")
parser.add_argument("--vertexai", action="store_true",
                    help="Use Google Vertex AI API instead of Gemini API (requires GOOGLE_CLOUD_PROJECT)")
args = parser.parse_args()

def list_openai_models():
    """List available OpenAI models"""
    try:
        import openai
    except ImportError:
        print("Error: openai package not installed. Install with: pip install openai")
        sys.exit(1)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set")
        sys.exit(1)

    print("Listing available OpenAI models...")
    print("=" * 80)

    try:
        client = openai.OpenAI(api_key=api_key)
        models = client.models.list()

        # Filter for main models (not fine-tuned versions)
        main_models = [m for m in models.data if not m.id.startswith("ft:")]

        for model in sorted(main_models, key=lambda x: x.id):
            print(f"Model: {model.id}")
    except Exception as e:
        print(f"Error listing models: {e}")
        sys.exit(1)


def list_google_models():
    """List available Google/Gemini models"""
    try:
        from google import genai
    except ImportError:
        print("Error: google-genai package not installed. Install with: pip install google-genai")
        sys.exit(1)

    # Set default region
    if args.region is None:
        args.region = "us-central1"

    if args.vertexai:
        # Use Vertex AI API with regional endpoints
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project:
            print("Error: GOOGLE_CLOUD_PROJECT not set (required for Vertex AI)")
            sys.exit(1)

        print(f"Using Vertex AI API with project: {project}, region: {args.region}")
        client = genai.Client(
            vertexai=True,
            project=project,
            location=args.region
        )
    else:
        # Use Gemini API key (no regional endpoints available)
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY not set")
            sys.exit(1)

        # Check if user explicitly specified a region
        if '--region' in sys.argv:
            print("Error: --region flag requires --use-vertexai")
            print("       Regional endpoints are only available with Vertex AI API.")
            print("       Either add --use-vertexai flag or remove --region flag.")
            sys.exit(1)

        client = genai.Client(api_key=api_key)

    if args.vertexai:
        print(f"Listing available models in {args.region}...")
    else:
        print(f"Listing available models in auto-selected region...")
    print("=" * 80)

    try:
        models = client.models.list()
        for model in models:
            # Check if it supports generateContent
            if hasattr(model, 'supported_generation_methods'):
                methods = model.supported_generation_methods
            else:
                methods = []

            print(f"Model: {model.name}")
            if methods:
                print(f"  Supported methods: {methods}")
    except Exception as e:
        print(f"Error listing models: {e}")
        print("\nTrying alternative approach...")

        # Try some known model names
        test_models = [
            "gemini-3.0-pro",
            "gemini-2.5-pro",
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ]

        for model_name in test_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents="Say hello"
                )
                print(f"✓ {model_name} - WORKS")
            except Exception as e:
                error_msg = str(e)
                if "404" in error_msg or "not found" in error_msg.lower():
                    print(f"✗ {model_name} - NOT FOUND")
                else:
                    print(f"? {model_name} - Error: {error_msg[:100]}")


def list_anthropic_models():
    """List available Anthropic models"""
    try:
        import anthropic
    except ImportError:
        print("Error: anthropic package not installed. Install with: pip install anthropic")
        sys.exit(1)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    print("Listing available Anthropic models...")
    print("=" * 80)

    # Anthropic doesn't have a list models API endpoint, so we list known models
    known_models = [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-sonnet-20240620",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
        "claude-2.1",
        "claude-2.0",
    ]

    print("Known Anthropic Claude models:")
    for model in known_models:
        print(f"Model: {model}")

    print("\nNote: Anthropic does not provide a models API endpoint.")
    print("This is a list of known models. Check https://docs.anthropic.com/en/docs/models-overview for the latest.")


def list_xai_models():
    """List available xAI models"""
    try:
        import openai
    except ImportError:
        print("Error: openai package not installed (xAI uses OpenAI-compatible API). Install with: pip install openai")
        sys.exit(1)

    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("Error: XAI_API_KEY not set")
        sys.exit(1)

    print("Listing available xAI models (xAI uses aliases, so grok-4 is an acceptable API name, resolving to grok-4-0709 as of Nov. 2025)...")
    print("=" * 80)

    try:
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
        models = client.models.list()

        for model in models.data:
            print(f"Model: {model.id}")
    except Exception as e:
        print(f"Error listing models: {e}")
        print("\nKnown xAI models:")
        print("Model: grok-beta")
        print("Model: grok-vision-beta")
        print("\nNote: Check https://docs.x.ai/docs for the latest model information.")


# Main execution
if args.provider == "OpenAI":
    list_openai_models()
elif args.provider == "Google":
    list_google_models()
elif args.provider == "Anthropic":
    list_anthropic_models()
elif args.provider == "xAI":
    list_xai_models()
