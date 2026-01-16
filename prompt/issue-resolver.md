@docs/project.md 에 있는 backlog 이슈의 번호를
입력 하면 해당 issue를 해소하는 일련의 개발 과정을 수행하는
pipeline을 기획하세요.
기획한 pipeline에 어떤 부분에서 skill, command, sub agents를 활용할지 context 비용 효율 측면에서 고민하세요.
그 뒤 /skill-creator, /agent-creator, /slash-command-creator를 호출하여 기획된 파이프라인을 구축할 예정이므로,
순서대로 어떤 프롬프트를 이용하여 해당 기능들을 구현할지 안내해주세요.

이제부터 제가 만들고자 하는 pipeline의 요구사항을 설명합니다.
issue를 해결하는 과정은 아래와 같은 순서를 따릅니다.

## 순서

1. 이슈를 해소하기 위한 기획사항 구체화

- /skill-loader를 활용하여 @docs/spec에 있는 문서를 적절히 context에 반영하여, 해당 이슈가 해결하고자 하는 문제가 무엇인지, 어떻게 해결할 것인지 구체적으로 기획하세요.
- 기획이 완료되면 나에게 확인을 받고, 주요한 의사결정 사항이 필요하면 나에게 최대 4개 까지 질문하며 이슈 해결 계획서를 작성하여 별도의 문서로 작성해두세요.

2. 기획문서 반영

- 1에서 결정되었거나 기존과 변경된 사항을 spec 문서와 /skill-loader에 반영하세요.

3. 이슈 해결 작업

- 이슈를 처리할 준비가 끝나면, /project-update를 이용하여 issue를 in progress로 이동하고 새로운 작업 브랜치를 생성하세요.
- 이제 1에서 생성한 이슈 해결 계획서와 /spec-loader를 적절히 활용하여 개발 작업을 수행하세요.

## version control guide

개발 작업은 주어진 테스트코드와 신규 테스트 코드 작성을 진행하며 RED-GREEN-REFACTOR 구조로 반복하여 진행합니다.
기획에 따라 먼저 테스트 코드를 기획하여 나에게 확인을 받으세요.
테스트코드도 관리 공수가 많이 들어가므로 edge case 위주로 계획하고, 1개 이상의 approval case를 포함하세요.
하나의 Red-Green-Refactor 작업이 끝나면 Commit을 생성하고, 이때 Commit의 변경사항이 100줄이 넘지 않도록 작업 규모를 작게 유지하세요.
만약 해당 브랜치에서의 작업이 800줄 이상의 변경사항이 발생한다면, 작업을 중지하고 후속 작업은 별도의 branch에서 수행해야 합니다.

부가적인 branch가 필요할때는 기존 작업은 PR을 생성후 /project-link-pr을 수행합니다. 이때 Code Review는 별도의 봇이 처리하므로, 내가 직접 /pr-review-resolver를 예정이니 작업을 중지하면 됩니다.
부가적인 branch는 직전 PR의 마지막 commit을 base로 하여 위의 작업 파이프라인을 그대로 따라합니다.
