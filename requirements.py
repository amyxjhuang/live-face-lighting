import streamlit as st
import numpy as np
import onnxruntime as rt
import mediapipe as mp
import os
import cv2
import av
from typing import List
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from twilio.rest import Client
from skimage.transform import SimilarityTransform
from types import SimpleNamespace
from sklearn.metrics.pairwise import cosine_distances