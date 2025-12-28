import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_no_image(self):
        matches = extract_markdown_images("This is text with no image")
        self.assertListEqual([], matches)

    def test_no_link(self):
        matches = extract_markdown_links("This is text with no link")
        self.assertListEqual([], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_only_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and an ![image](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def text_extract_only_image(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev) and an ![image](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)


if __name__ == "__main__":
    unittest.main()
