# WeChat Login
This is a proof of concept project showing the capability to log users in by scanning the QR code and follow WeChat public accounts.
The project is mainly composed of the following steps.

1) Built a SAE (Sina App Engine) server to receive http request
2) Generate customized QR code, which Wechat users can scan to follow WeChat public account
3) Upon scan of the QR code, Wechat pushs a http request to the server with user ID
4) Process the user ID to extract user info
