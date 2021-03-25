from kivy.resources import resource_add_path
from kivy.lang import Builder
from pathlib import Path
from ui import LaternaMagica

if __name__ == '__main__':
    Builder.load_file(str(Path(__file__).parent / 'ui' / 'kv_lang' / 'laterna_magica.kv'))
    LaternaMagica().run()
