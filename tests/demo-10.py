import os
def Is64Windows():
    return 'PROGRAMFILES(X86)' in os.environ

print(Is64Windows())