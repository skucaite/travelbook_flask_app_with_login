import os
import secrets
# import babel
from PIL import Image
from flask import render_template, url_for, flash, request, redirect, abort
from travelbook import app, db, bcrypt, mail
from travelbook.forms import (TravelForm, GuideForm, RegistrationForm, LoginForm,
                    RequestResetForm, ResetPasswordForm)
from travelbook.models import Guide, Travel
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
