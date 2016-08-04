from django import forms
from .models import Party
import spotipy
import spotipy.oauth2 as oauth2
from django.conf import settings

def get_user_playlists(user):
    user = user.social_auth.get(provider='spotify')
    sp_oauth = oauth2.SpotifyOAuth(settings.SPOTIPY_CLIENT_ID,
                                   settings.SPOTIPY_CLIENT_SECRET,
                                   settings.SPOTIPY_REDIRECT_URI,
                                   scope=settings.SOCIAL_AUTH_SPOTIFY_SCOPE[0])
    new_token_info = sp_oauth._refresh_access_token(user.extra_data['refresh_token'])
    token = new_token_info['access_token']
    cleaned_playlists = [(unicode("UpNext - Start a new playlist"), unicode("Start a new playlist"))]
    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(user)["items"]
        for playlist in playlists:
            if playlist["owner"]["id"] == unicode(user):
                cleaned_playlists.append((playlist['uri'], playlist['name']))
    return cleaned_playlists


class PartyForm(forms.ModelForm):
    required_css_class = "required"
    error_css_class = "error"


    def __init__(self, user, *args, **kwargs):
        super(PartyForm, self).__init__(*args, **kwargs)
        self.fields['uri'] = forms.ChoiceField(
            choices=get_user_playlists(user))


    class Meta:
        model = Party
        fields = ('party_name', 'url', 'user_nickname', 'min_score', 'uri',)


class ScoreForm(forms.ModelForm):
    required_css_class = "required"
    error_css_class = "error"

    class Meta:
        model = Party
        fields = ('min_score',)
