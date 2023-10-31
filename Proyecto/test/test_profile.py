import pytest
import sys
import os
from flask import Flask, url_for
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ui import auth_bp
from main import app
from flask import Flask, render_template_string

