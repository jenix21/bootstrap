# Concept

## Source Stamps

용어 구분
- repository : 코드 저장소.
- codebase : 여러 repository 로 구성.
- version (revision) : codebase 의 소스 버전.
- project : 여러 codebase 로 구성.

Buildbot 은 어떤 **버전**의 codebase 를 빌드할지 알아야 함.
- 각각의 codebase 에 대해 **source stamp** 사용.
- project 는 **source stamp set** 을 필요로 함. (sourcestamps 모음)

## Version Control Systems

VCS 를 추상화 해서 사용.

빌드 수행시기 판단.
1. **change sources** 가 저장소 모니터링.
2. 저장소에 대한 변경을 **changes** 로 표현.

**change sources** category
- pollers : 주기적으로 저장소 체크.
- hooks : 저장소에 변경이 발생하면 buildbot 으로 알려줌.

scheduler
- 빌드를 위해 설정에 따라 source stamp set 준비.

1개 이상의 source steps 은 source stamp set 사용.

### Tree Stability

buildmaster 에게 여러개의 changes 가 도착하는 경우도 있음.
(하나의 feature 를 위해 여러번 commit 할때)

tree stability
- 매번 changes 가 도작할 때마다 빌드를 하지 않기 위한 개념.
- timer 를 사용해서, 일정 시간 동안 changes 가 없으면 빌드하도록 함.

### How Different VC Systems Specify Sources

source step
- 나의 static repourl 지정. (repository 의 위치)

branch parameter 
- default master branch 에서 코드를 가져오지 않음.

revision 
- SHA1 hash 로 지정 (git rev-parse)

## Changes

Change instance 의 각 속성을 설명함.

### Who

who 속성 
- 변경한 사람.
- who 속성은 buildbot 의 DB 에 저장됨. ([User Objects](http://goo.gl/s3NA5y), 현재 Git 만 저장됨)

StatusNotifier 
- who 속성을 mapping 할 수 있음. (이메일 주소, IRC 핸들, 등)

### Files

추가, 삭제, 수정된 파일 리스트.

Scheduler.fileIsImportant() 함수에서 사용 가능.
- 빌드를 할지 말지 결정함.
- 예) C 파일이 변경된 경우만 빌드.
```python
def has_C_files(change):
  for name in change.files:
    if name.endswith('.c'):
      return True
  return False
```

BuildStep 에서 사용 가능.
- 특정 파일이 있는지 여부를 확인해 추가 작업(테스트 등) 수행 가능.

### Comments

commit 메세지

### Project

change 의 속성이기도 하지만 source stamp 갖고 있음.

해당 project 를 의미하는 짧은 문자열, 여러 프로젝트가 하나의 buildmaster 를 통해 빌드 될때 유용함.

### Repository

변경이 일어난 저장소.

### Codebase

변경이 일어난 codebase. (repository 가 달라도 codebase 가 같을 수 있음)

default 로 값이 없으며, codebaseGenerator 설정으로 mapping 할 수 있음.

```python
all_repositories = {
    r'https://hg/hg/mailsuite/mailclient': 'mailexe',
    r'https://hg/hg/mailsuite/mapilib': 'mapilib',
    r'https://hg/hg/mailsuite/imaplib': 'imaplib',
    r'https://github.com/mailinc/mailsuite/mailclient': 'mailexe',
    r'https://github.com/mailinc/mailsuite/mapilib': 'mapilib',
    r'https://github.com/mailinc/mailsuite/imaplib': 'imaplib',
}

def codebaseGenerator(chdict):
    return all_repositories[chdict['repository']]

c['codebaseGenerator'] = codebaseGenerator
```

### Revision

Git 의 경우 SHA1 hash 을 나타내는 짧은 문자열 (git rev-parse)

### Branches

Scheduler 에서 해당 branch 를 빌드 할지 결정할 수 있음.

branch='warner-newfeature', files=['src/foo.c']

## Scheduling Builds

buildmaster 는 여러 개의 Scheduler 객체를 갖고 있음.

Scheduler
- 유입된 Change 의 복사본을 참조.
- 언제 Build 가 수행되면 좋을지 결정할 책임이 있음.
- 여러 목적으로 사용할 수 있음.
- tree stable timer 설정 가능.
- 여러 조건으로 관심있는 변경만 필터링 할 수 있음. (파일, branch 등)

예)
- quick scheduler : 명백한 오류가 있을 때, 개발자에게 빠른 피드백을 주기 위함. 전체 테스트를 돌리거나 다른 플랫폼 빌드를 수행하지 않음.
- full schedule : 미묘한 문제를 찾기 위해 포괄적인 테스트 수행, quick scheduler 수행 후 실행되도록 할 수 있음. 여러 Builder 를 fedding 하기도 함.

Build coordination
- build 사이에 dependency 설정.
- 테스트가 모두 성공한 package 만 빌드.

Periodic Scheduler subclass
- N 초마다 수행됨.

Scheduler -(생성)-> BuildSet -> BuildMaster -(생성)-> BuildRequests -> Builders

buildmaster config 설정에서 c['schedulers'] list 에 Scheduler instance 가 추가되면 활성화됨.

## BuildSets

Builder - BuildSet - Builds - Steps

하나의 단위로 추적되며, 포함된 어떤 Build 라도 fail 이면 fail 처리됨.

알림 메세지 유형
- firstFailure type : 실패하면 바로 옴.
- Finished type : 성공 실패 상관 없이 끝나는 경우.

BuildSet 생성 with ..
- 하나 이상의 source stamp tuples (branch, revision, changes, patch)
- Builder 목록.

## BuildRequests

하나의 Builder 에게 전달되는 요청으로써, 빌드할 소스코드 집합을 포함 (하나 이상의 soruce stamps)

Builder 는 buildslave 가 free 상태이면 BuildRequest 를 수행함.

BuildRequest
- codebase 당 하나의 SourceStamp specification 포함.
- Build 객체가 일련의 Step 들을 실행하는 형태로 빌드 진행.
- (변경 예정) Build 는 what gets built 정의, 별도의 BuildProcess (Builder 가 제공) 가 how it gets built 정의.
- 다른 compatible BuildRequest 와 합쳐질 수 있음.
- 일반적으로 도착한 Change 에 의한 Build 는 합쳐질 수 있음.
- 사용자 요청에 의한 Build 는 합쳐질 수 없음. (단, 같은 branch 의 최근 소스를 빌드하기 위해 여러번 요청이 있는 경우는 괜찮음.)

## Builders

Buildmaster -(run)-> Builders, 한 개 이상의 build slaves 에서 한 종류의 빌드 수행.

Builder 는 ..
- long-live object 이며, 설정 파일이 parsing 되면 생성됨.
- build slaves 와 연결 중재.
- Build 객체 생성.
- 유일한 이름.
- 상태 정보를 저장할 buildmaster-side 디렉토리 경로.
- 실제 작업을 수행할 buildslave-side 디렉토리 경로.

## Build Factories

builder 는 BuildFactory 를 갖고 있고, Build instance 를 생성함.

## Build Slaves

각 builder 는 하나 이상의 BuildSlave 와 연관됨.

## Builds

build 는 하나의 컴파일 이나 테스트 수행 단위, 여러 step 으로 구성됨.

BuildFactory 에 Step 을 추가하고, Builder 에서는 BuildFactory 를 통해서 Build 객체를 받음.

## Users

Change 에 포함된 who 속성으로 참조만 하고 있음.

권한 레벨에 따라 web interface 나 IRC 에서 명령을 수행할 수 있음.

### User Objects

사용자와 다양한 interaction 수행 가능.

### Changes

who 속성은 VCS 에 따라 다르게 formatting 됨.

### Tools

buildbot user 명령어로 user 의 속성 변경 가능.

### Users

User Objects 활용
- web authentication 을 위해 UsersAuth 사용 (WebStatus 참고)
- buildbot user 로 bb_username, bb_password 설정.

### Doing Things With Users

사용자 목록 - blamelist, interested users

### Email Addresses

MailNotifier 
- status target 의 한 종류, 빌드 결과를 메일로 보냄.
- email address 목록을 받을 수 있음.
- Build's Interested Users 에게 보내도록 설정 할 수도 있음.

EmailLookup
- MailNotifier 생성시 전달하지 않으면, User Objects 에서 메일 주소를 찾음.
- 주소 문자열만 전달하면, EmailLookup.getAddress(이름) 으로 변환시 문자열만 뒤에 붙임.
- extraRecipients argument : 추가 수신자 지정.
- lookup argument : 복잡한 처리를 위해 EmailLookup 객체 지정.

### IRC Nicknames

buildbot.status.words.IRC
- status target
- IRCLookup for nicknames

### Live Status Clients

desktop status client interface 제공.

## Build Properties

각 build 에 하나의 Build Properties 집합이 있음.
- 속성에 따라 build steps 을 다르게 할 수 있음.
- key-value pairs.
- variable 형태로 존재하고, 빌드 실행시 생성되고 진행 중 값이 변하는 형태로 처리됨.
- 값은 여러 타입이며 기본적으로 json 으로 표현될 수 있음.

예)
- got_revision 속성 : revision 기록, 나중에 빌드된 tarball 파일 이름에 사용.
- codebase 가 여러개인 경우, got_revision 은 codebase 이름이 key 인 dictionary.
- is_nightly 속성 : nightly 빌드 체크.

## Multiple-Codebase Builds

설정
- codebase generator : codebaseGenerator 사용.
- scheduler : 프로젝트 빌드를 위해 필요한 모든 codebases 를 명시.
- multiple source steps(one for each codebase) : build factory 는 각 codebase 를 위한 source step 을 포함해야 함.
- build 를 위한 source stamp set 에서 적절한 source stamp 를 선택하기 위해 codebase 속성 사용.

***