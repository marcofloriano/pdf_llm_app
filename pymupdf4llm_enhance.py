import fitz

def to_dict_for_llm(self):
    return {
        "blocks": [
            {
                "type": block["type"],
                "bbox": block["bbox"],
                "lines": [
                    {
                        "bbox": line["bbox"],
                        "spans": [
                            {
                                "text": span["text"],
                                "bbox": span["bbox"],
                                "font": span["font"],
                                "size": span["size"],
                                "flags": span["flags"],
                                "color": span["color"],
                                "origin": span.get("origin"),
                                "bold": bool(span["flags"] & 2),
                                "italic": bool(span["flags"] & 1),
                                "underline": bool(span["flags"] & 4),
                            }
                            for span in line["spans"]
                        ],
                    }
                    for line in block.get("lines", [])
                ],
            }
            for block in self.get_text("dict")["blocks"]
        ]
    }

fitz.Page.to_dict_for_llm = to_dict_for_llm
