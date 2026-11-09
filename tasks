def format_text(text, width=70):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if not word:
            continue
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current = current + " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return "\n".join(lines)


if __name__ == "__main__":
    example = ("«Улучшение ежедневной работы даже важнее, чем выполнение ее». Вся суть Третьего пути в том, чтобы убедиться: мы постоянно работаем с системой, мы закрепляем полезные привычки и занимаемся совершенствованием чего-либо.")
    print(format_text(example, 70))
