
#!/usr/bin/env python3
"""Monthly official CFP checker. Generates review issue; never invents dates."""
import datetime as dt, hashlib, json, os, re, urllib.request, urllib.error
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
items=json.loads((ROOT/'conferences.json').read_text())
now=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d')
lines=[f'## Monthly conference CFP review — {now}', '',
       '공식 페이지의 현재 상태를 점검한 결과입니다. **날짜 변경을 자동 확정하지 않습니다.**',
       '공식 CFP를 검토하고 `conferences.json`에서 회차, 제출 마감일, 개최지를 수정하세요.', '']
for c in items:
    url=c.get('cfp') or c.get('url')
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'ConferenceInfoMonitor/1.0 (monthly link check)'})
        with urllib.request.urlopen(req,timeout=12) as resp:
            body=resp.read(300000).decode('utf-8','ignore')
            final=resp.geturl(); status=resp.status
        # HTML tags removed; text is untrusted reference material, not automatically written to data.
        title_match=re.search(r'<title[^>]*>(.*?)</title>',body,re.I|re.S)
        title=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',title_match.group(1))).strip()[:130] if title_match else 'no title'
        title=title.replace('\n',' ')
        lines.append(f'- **{c["id"]} {c["year"]}**: HTTP {status} · {title} · [공식 CFP]({final})')
    except Exception as e:
        lines.append(f'- **{c["id"]}**: 접속 확인 실패 ({type(e).__name__}) · [공식 CFP]({url})')
lines.extend(['','### 검토 우선순위','현재 회차 마감일이 지났거나 미확인(TBA)인 학회부터 다음 연도 CFP를 확인하세요.'])
body='\n'.join(lines)
print(body)
repo=os.getenv('GH_REPO'); token=os.getenv('GH_TOKEN')
if repo and token:
    title=f'Conference CFP monthly review — {now[:7]}'
    payload=json.dumps({'title':title,'body':body,'labels':[]}).encode()
    req=urllib.request.Request(f'https://api.github.com/repos/{repo}/issues',data=payload,headers={'Authorization':f'Bearer {token}','Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'ConferenceInfoMonitor','Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=15) as response:
        print('Created issue:',json.loads(response.read())['html_url'])
