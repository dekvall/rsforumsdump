from setuptools import setup
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(name='rsforumsdump',
      version='1.0.0',
      description='A tool for dumping rsforums threads for archival purposes',
      url='https://github.com/dekvall/rsforumsdump',
      entry_points={'console_scripts': ['rsforumsdump=rsforumsdump.__main__:main']},
      keywords=['rs','osrs','forums', 'rsforums', 'archival'],
      author='dekvall',
      author_email='dkvldev@gmail.com',
      license='MIT',
      packages=['rsforumsdump'],
      install_requires=reqs
      )

