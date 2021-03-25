import pytest


# web
pytest.main(["-s", "-v", "-P=B", "-E=test", "-M=WEB", "--screenshot=on", "--screenshot_path=on", #"-m=login",
             "-n=4", "--dist=loadscope", "-S=DEBUG"])

# app
# pytest.main(["-sv", "-M=APP", "-E=test", "-P=G", "-S=DEBUG", "--screenshot=on", "--screenshot_path=on",
# "--device=samsung-10"])/
# pytest.main(["-sv", "-M=APP", "-E=test", "-P=G", "-S=HUB", "--screenshot=on", "--screenshot_path=on", "-n=2",
#              "--dist=loadscope"])