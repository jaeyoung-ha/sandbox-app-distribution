# 사내 앱 배포 가이드 아키텍처 다이어그램 생성 스크립트
# 실행: python3 architecture_diagram.py  ->  architecture.png 생성
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import CloudFront
from diagrams.aws.compute import Lambda
from diagrams.aws.security import Cognito, SecretsManager
from diagrams.aws.mobile import Amplify
from diagrams.onprem.client import Users

# 다이어그램 전역 속성
graph_attr = {
  "fontsize": "16",
  "bgcolor": "white",
  "pad": "0.6",
  "splines": "spline",
}

with Diagram(
  "사내 앱 배포 인증 아키텍처",
  filename="architecture",
  outformat="png",
  show=False,
  direction="LR",
  graph_attr=graph_attr,
):
  users = Users("사용자")

  # us-east-1: Lambda@Edge만 필수 (CloudFront는 글로벌)
  with Cluster("us-east-1 (필수) · CloudFront는 글로벌"):
    cf = CloudFront("CloudFront\n(글로벌 배포)")
    edge = Lambda("Lambda@Edge\nviewer:인증확인\norigin:Host교정+BasicAuth")

  # ap-northeast-2(서울): 나머지 리소스
  with Cluster("ap-northeast-2 (서울)"):
    cognito = Cognito("Cognito\n호스팅 로그인")
    secrets = SecretsManager("Secrets Manager\n(Basic Auth 자격증명)")
    amplify = Amplify("Amplify 앱\n(Basic Auth로 잠금)")

  # 요청 흐름
  users >> Edge(label="① 접속") >> cf
  cf >> Edge(label="② 인증 확인", style="dashed") >> edge
  edge >> Edge(label="③ 미인증 시 리다이렉트", color="firebrick", style="dashed") >> cognito
  cognito >> Edge(label="④ 로그인 후 쿠키 발급·복귀", color="firebrick", style="dashed") >> cf
  edge >> Edge(label="자격증명 조회(크로스 리전)") >> secrets
  cf >> Edge(label="⑤ 인증 통과 → 오리진 요청", color="darkgreen") >> amplify
