"""用户API接口测试模块"""

import pytest
import allure


@allure.feature("用户接口")
@allure.story("查询用户")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_001 查询所有用户")
def test_查询所有用户(api):
    """查询所有用户，验证返回10个用户及数据结构"""
    with allure.step("发送 GET 请求"):
        response = api.get(f"{api.base_url}/users")

    with allure.step("验证状态码"):
        assert response.status_code == 200

    with allure.step("验证响应时间"):
        assert response.elapsed.total_seconds() < 2

    with allure.step("验证响应数据结构"):
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 10

    with allure.step("验证每个用户都有关键字段"):
        for user in data:
            assert "id" in user
            assert "name" in user
            assert "email" in user


@allure.feature("用户接口")
@allure.story("查询用户")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_002 查询单个用户")
def test_查询单个用户(api):
    """查询ID为1的用户，验证返回正确的用户信息"""
    with allure.step("发送 GET 请求"):
        response = api.get(f"{api.base_url}/users/1")

    with allure.step("验证状态码"):
        assert response.status_code == 200

    with allure.step("验证响应数据"):
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Leanne Graham"
        assert data["email"] == "Sincere@april.biz"


@allure.feature("用户接口")
@allure.story("查询用户")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC_003 查询不存在的用户")
def test_查询不存在的用户(api):
    """查询不存在的用户ID，验证返回404"""
    with allure.step("发送 GET 请求"):
        response = api.get(f"{api.base_url}/users/9999")

    with allure.step("验证状态码"):
        assert response.status_code == 404

    with allure.step("验证响应数据"):
        data = response.json()
        assert data == {}


@allure.feature("用户接口")
@allure.story("创建用户")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_004 创建新用户")
def test_创建新用户(api):
    """创建新用户，验证返回201及用户信息"""
    with allure.step("准备要发送的数据"):
        new_user = {
            "name": "Tom",
            "email": "tom@test.com"
        }

    with allure.step("发送 POST 请求"):
        response = api.post(f"{api.base_url}/users", json=new_user)

    with allure.step("验证状态码"):
        assert response.status_code == 201

    with allure.step("验证响应数据"):
        data = response.json()
        assert data["name"] == "Tom"
        assert data["email"] == "tom@test.com"
        assert "id" in data


@allure.feature("用户接口")
@allure.story("修改用户")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_005 修改用户")
def test_修改用户(api):
    """修改用户信息，验证返回更新后的数据"""
    with allure.step("准备要修改的数据"):
        update_data = {
            "name": "Tom Updated"
        }

    with allure.step("发送 PUT 请求"):
        response = api.put(f"{api.base_url}/users/1", json=update_data)

    with allure.step("验证状态码"):
        assert response.status_code == 200

    with allure.step("验证响应数据"):
        data = response.json()
        assert data["name"] == "Tom Updated"


@allure.feature("用户接口")
@allure.story("删除用户")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC_006 删除用户")
def test_删除用户(api):
    """删除用户，验证返回200"""
    with allure.step("发送 DELETE 请求"):
        response = api.delete(f"{api.base_url}/users/1")

    with allure.step("验证状态码"):
        assert response.status_code == 200

    with allure.step("验证响应数据"):
        data = response.json()
        assert data == {}
