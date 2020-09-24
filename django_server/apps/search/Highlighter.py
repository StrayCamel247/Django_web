from django.utils.html import strip_tags
from haystack.utils import Highlighter as HaystackHighlighter


class Highlighter(HaystackHighlighter):
    """
    自定义关键词高亮器，不截断过短的文本（例如文章标题）
    """
    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        if len(text_block) < self.max_length:
            start_offset = 0
        return self.render_html(highlight_locations, start_offset, end_offset)
    #关键代码是：if len(text_block) < self.max_length:，start_offset 是 haystack 根据关键词算出来第一个关键词在文本中出现的位置。max_length 指定了展示结果的最大长度。我们在代码中做一个判断，如果文本内容 text_block 没有超过允许的最大长度，就将 start_offset 设为 0，这样就从文本的第一个字符开始展示，标题这种短文本就不会被截断了。