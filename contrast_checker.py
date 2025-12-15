def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_relative_luminance(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def get_contrast_ratio(lum1, lum2):
    if lum1 > lum2:
        return (lum1 + 0.05) / (lum2 + 0.05)
    else:
        return (lum2 + 0.05) / (lum1 + 0.05)

def check_wcag_compliance(contrast_ratio):
    print(f"Contrast Ratio: {contrast_ratio:.2f}:1")
    print("\n--- WCAG Compliance ---")
    # Normal Text
    if contrast_ratio >= 7:
        print("Normal Text: AAA (Pass)")
    elif contrast_ratio >= 4.5:
        print("Normal Text: AA (Pass)")
    else:
        print("Normal Text: Fail")
        
    # Large Text (18pt or 14pt bold)
    if contrast_ratio >= 4.5:
        print("Large Text: AAA (Pass)")
    elif contrast_ratio >= 3:
        print("Large Text: AA (Pass)")
    else:
        print("Large Text: Fail")

import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python contrast_checker.py <color1_hex> <color2_hex>")
        sys.exit(1)

    color1_hex = sys.argv[1]
    color2_hex = sys.argv[2]

    color1_rgb = hex_to_rgb(color1_hex)
    color2_rgb = hex_to_rgb(color2_hex)

    lum1 = get_relative_luminance(color1_rgb)
    lum2 = get_relative_luminance(color2_rgb)

    contrast = get_contrast_ratio(lum1, lum2)
    
    check_wcag_compliance(contrast)
