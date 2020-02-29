#!/usr/bin/env python
import os
from app import create_app, db


config = os.environ.get('CONFIG')
app = create_app(config)


if __name__ == '__main__':
	app.run()
