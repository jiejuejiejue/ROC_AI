import axios from "axios";
import { ElMessage } from "element-plus";

const baseURL = 'http://127.0.0.1:8888/api/';

// 获取用户信息接口
export const fetchUserInfo = (email) => {
    return axios.get(baseURL + 'userinfo', {
        params: { email: email }
    }).then(response => response.data)
        .catch(error => {
            console.error('Error fetching user info:', error);
            throw error;
        });
};


// 上传头像的 API 函数
export const uploadAvatar = (formData, callback) => {
    axios.post(`${baseURL}upload-avatar`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
        .then(response => {
            callback(response);
        })
        .catch(error => {
            console.error('上传头像失败:', error);
        });
};

// 登录接口
export const login = (username, password) => {
    console.log('Sending login request with:', username, password);
    return axios.post(baseURL + 'login', new URLSearchParams({
        username: username,
        password: password
    }), {
        headers: {
            'content-type': 'application/x-www-form-urlencoded'
        }
    });
};

// 注册接口
export const register = (registerForm, callback) => {
    axios.post(baseURL + 'register', new URLSearchParams({
        username: registerForm.username,
        password: registerForm.password,
        email: registerForm.email,
        verificationCode: registerForm.verificationCode
    }), {
        headers: {
            'content-type': 'application/x-www-form-urlencoded'
        }
    }).then((response) => {
        callback(response);
    }).catch((err) => {
        ElMessage.error('注册请求失败');
        console.error(err);
    });
};