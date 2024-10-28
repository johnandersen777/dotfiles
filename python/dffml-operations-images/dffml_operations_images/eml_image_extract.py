import argparse
import email
import os
import pathlib
import shutil
import subprocess
import tempfile
from email import policy
from email.parser import BytesParser
from pathlib import Path


import snoop

@snoop
def extract_images(eml_path: Path, output_dir: Path):
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(eml_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    image_count = 0

    # Walk through email parts and extract images
    for part in msg.iter_attachments():
        if part.get_content_maintype() == "image":
            # Save the image temporarily
            image_data = part.get_payload(decode=True)
            temp_image_path = output_dir / f"image_{image_count}.{part.get_content_subtype()}"
            temp_image_path.write_bytes(image_data)

            # Run exiftool in Docker to strip metadata
            output_image_path = output_dir / temp_image_path.name
            docker_command = [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{output_dir}:/tmp/images:z",
                "--entrypoint",
                "exiftool",
                "exiftool",
                "-all=",
                f"/tmp/images/{temp_image_path.name}",
            ]

            subprocess.run(docker_command, check=True)
            image_count += 1

    print(f"Extracted and processed {image_count} images to {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract images from .eml file and remove metadata."
    )
    parser.add_argument("eml_file", type=Path, help="Path to the .eml file")
    parser.add_argument(
        "output_dir", type=Path, help="Directory to save processed images"
    )

    args = parser.parse_args()

    extract_images(args.eml_file, args.output_dir)


if __name__ == "__main__":
    main()
