# https://docs.open.alipay.com/api_1/alipay.trade.page.pay/
# Crypto 需要安装 pip install pycryptodome
import json
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus, urlparse, parse_qs
from base64 import decodebytes, encodebytes


class AliPay(object):
    """
    支付宝支付接口
    """

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url
        # 私钥
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url
        with open(self.app_private_key_path) as fp:
            # 引入密钥 需要固定格式
            self.app_private_key = RSA.importKey(fp.read())
        # 公钥
        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.import_key(fp.read())

        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        # 请求参数
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # "qr_pay_mode":4
        }
        # 允许传递更多参数，放到biz_content
        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        # build_body主要生产消息的格式
        # 公共请求参数
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        # 签名
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        # 排完序后拼接起来
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        # 这里得到签名的字符串
        sign = self.sign(unsigned_string.encode("utf-8"))
        # 对url进行处理
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    # 参数传进来一定要排序
    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        # 签名的对象
        signer = PKCS1_v1_5.new(key)
        # 生成签名
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        """
        与阿里的密匙进行验证
        """
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        # 解码验证
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        """
        验证返回的url中数据是否正确
        然后再传入阿里验证
        """
        # 删除不需要的数据
        if "sign_type" in data:
            data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        # 重新构建请求参数
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


if __name__ == "__main__":
    # 用于反向验证
    return_url = 'http://47.98.34.221:8888/?charset=utf-8&out_trade_no=20191112&method=alipay.trade.page.pay.return&total_amount=100.00&sign=nLV4FE4nUmrp%2FuCiPALE5p0g7cZMi2QLyTe3rh3ft867cPF07FRVrHQwobKQadGas2uCOQl%2Fyrn2DXKKhbw2BT3JFkriVBqzUH%2B82fjsSbKfhe%2FgdI1w0KmKwaBOshqltlgnlCi%2FRDzzRpqXrgdBFscQm1Gd69RRNAAXok%2FglDxUnMVBPC54ZibR1vLzhI8321BkwWBRV3aXDha%2F8iGb7N8sUad17hK3SPYC6i6qQkYqBg2QO62zxapSquNg2hy0oNaQq1FufleobcJTGPC3DioJotoZx5BDGWulp32PehYPXa5UNQ8MLh0ZKfP8CuJN6fFhqeba95%2BZ7iAk3xkzNA%3D%3D&trade_no=2019121222001431861000298520&auth_app_id=2016092600599306&version=1.0&app_id=2016092600599306&sign_type=RSA2&seller_id=2088102177324690&timestamp=2019-12-12+15%3A58%3A00'
    o = urlparse(return_url)
    query = parse_qs(o.query)
    processed_query = {}
    # 获得sign 并从 返回的url在删除
    ali_sign = query.pop("sign")[0]

    # 测试用例
    alipay = AliPay(
        # 沙箱里面的appid值
        appid="2016092600599306",
        # notify_url是异步的url 比 reuturn_url 还重要
        app_notify_url="http://47.98.34.221:8888/api/alipay/return",  #
        # 我们自己商户的密钥
        app_private_key_path="../trade/keys/private_2048.txt",
        # 支付宝的公钥
        alipay_public_key_path="../trade/keys/alipay_key_2048.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        # debug为true时使用沙箱的url。如果不是用正式环境的url
        debug=True,  # 默认False,
        return_url="http://47.98.34.221:8888/api/alipay/return"  # 支付成功之后导向地址
    )
    # 支付宝返回数据之后我们需要验证一下是否被人获取篡改
    # 支付成功之后验证的过程与生成过程刚好相反
    # query返回的字典的值为list所以这里取出list
    for key, value in query.items():
        processed_query[key] = value[0]
    print(alipay.verify(processed_query, ali_sign))

    # 直接支付:生成请求的字符串。
    url = alipay.direct_pay(
        # 订单标题
        subject="测试订单",
        # 我们商户自行生成的订单号
        out_trade_no="20191123",
        # 订单金额
        total_amount=100,
        # 成功付款后跳转到的页面，return_url同步的url
        return_url="http://47.98.34.221:8888/api/alipay/return"  # 支付成功之后导向地址
    )
    # 将生成的请求字符串拿到我们的url中进行拼接
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

    print(re_url)
