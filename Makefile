APP=pedialabsnew
JS_FILES=media/js/quizshow.js media/js/sidemenu.js media/stick.js
MAX_COMPLEXITY=7

all: jenkins

include *.mk

eslint: $(JS_SENTINAL)
	$(NODE_MODULES)/.bin/eslint $(JS_FILES)

.PHONY: eslint
