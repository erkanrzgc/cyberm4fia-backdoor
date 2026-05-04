def print_gradient_banner():
    banner = r'''
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███╗   ███╗██╗  ██╗███████╗██╗ █████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗████╗ ████║██║  ██║██╔════╝██║██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██╔████╔██║███████║█████╗  ██║███████║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║╚██╔╝██║╚════██║██╔══╝  ██║██╔══██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║ ╚═╝ ██║     ██║██║     ██║██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ 
'''
    lines = banner.strip('\n').split('\n')
    start_color = (230, 230, 230)
    end_color = (40, 40, 40)

    steps = len(lines)
    for i, line in enumerate(lines):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / steps))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / steps))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / steps))
        print(f"\x1b[38;2;{r};{g};{b}m{line}\x1b[0m")
    print()
