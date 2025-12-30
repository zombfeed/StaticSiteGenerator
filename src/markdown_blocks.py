from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5


def block_to_block_type(block):
    block_type = BlockType.PARAGRAPH
    if block.startswith("######"):
        block_type = BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        block_type = BlockType.CODE
    else:
        is_incrementing = 1
        previous = BlockType.PARAGRAPH
        lines = block.split("\n")
        for i in range(len(lines)):
            if lines[i].startswith(">"):
                if i == 0:
                    previous = BlockType.QUOTE

                block_type = (
                    BlockType.QUOTE
                    if previous != BlockType.PARAGRAPH
                    else BlockType.PARAGRAPH
                )
            elif lines[i].startswith("- "):
                if i == 0:
                    previous = BlockType.UNORDERED_LIST
                block_type = (
                    BlockType.UNORDERED_LIST
                    if previous != BlockType.PARAGRAPH
                    else BlockType.PARAGRAPH
                )
            elif lines[i][0].isdigit() and int(lines[i][0]) == is_incrementing:
                if lines[i].startswith(f"{lines[i][0]}. "):
                    is_incrementing += 1
                    block_type = BlockType.ORDERED_LIST
                else:
                    block_type = BlockType.PARAGRAPH
            else:
                block_type = BlockType.PARAGRAPH
    return block_type


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n")]


if __name__ == "__main__":
    md = "```this is a code block```"
    md2 = "```this is a code block\nwith multiple lines```"
    print(block_to_block_type(md))
    print(block_to_block_type(md2))
