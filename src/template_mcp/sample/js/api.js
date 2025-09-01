import request from '@/utils/request'

// 查询AI提示词内容管理列表
export function listPrompt(query) {
    return request({
        url: '/system/prompt/list',
        method: 'get',
        params: query
    })
}

// 查询AI提示词内容管理详细
export function getPrompt(id) {
    return request({
        url: '/system/prompt/info/' + id,
        method: 'get'
    })
}

// 新增AI提示词内容管理
export function addPrompt(data) {
    return request({
        url: '/system/prompt/add',
        method: 'post',
        data: data
    })
}

// 修改AI提示词内容管理
export function updatePrompt(data) {
    return request({
        url: '/system/prompt/edit',
        method: 'post',
        data: data
    })
}

// 删除AI提示词内容管理
export function delPrompt(id) {
    return request({
        url: '/system/prompt/remove/' + id,
        method: 'post'
    })
}

// 批量删除AI提示词内容管理
export function batchDelPrompt(data) {
    return request({
        url: '/system/prompt/batchRemove',
        method: 'post',
        data: data
    })
}
