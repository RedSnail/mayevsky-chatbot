import setuptools

install_requires=[
   'vk_api',
]

setuptools.setup(
    name="mayevsky-chatbot",
    use_scm_version = True,
    setup_requires=['setuptools_scm'],    author="RedSnail",
    author_email="",
    description="The bot for TheBigMayevsky",
    url="https://github.com/RedSnail/mayevsky-chatbot",
    packages=setuptools.find_packages(),
    install_requires=install_requires
)
