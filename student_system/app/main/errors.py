from flask import render_template, request, jsonify, flash, redirect, url_for
from . import main
import logging
import traceback

# 配置日志记录器
logger = logging.getLogger(__name__)

def create_error_response(error_code, error_name, error_description, error_details=None):
    """创建统一的错误响应"""
    # 如果是AJAX请求，返回JSON响应
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response_data = {
            'error': error_name,
            'message': error_description,
            'code': error_code
        }
        if error_details:
            response_data['details'] = error_details
        
        response = jsonify(response_data)
        response.status_code = error_code
        return response
    
    # 对于普通请求，渲染错误页面
    return render_template(
        'errors/generic.html',
        error_code=error_code,
        error_name=error_name,
        error_description=error_description,
        error_details=error_details
    ), error_code

@main.app_errorhandler(404)
def page_not_found(e):
     """处理404页面未找到错误"""
     logger.warning(f"404错误 - 请求的页面不存在: {request.url}")
     return create_error_response(
         404, 
         '页面未找到', 
         '请求的页面不存在，请检查URL是否正确。',
         f"请求路径: {request.url}"
     )

@main.app_errorhandler(500)
def internal_server_error(e):
    """处理500服务器内部错误"""
    logger.error(f"500错误 - 服务器内部错误: {str(e)}")
    # 在开发环境中显示详细错误信息
    error_details = None
    from flask import current_app
    if current_app.debug:
        error_details = traceback.format_exc()
    
    return create_error_response(
        500,
        '服务器内部错误',
        '服务器遇到意外错误，请稍后重试。',
        error_details
    )

@main.app_errorhandler(403)
def forbidden(e):
    """处理403禁止访问错误"""
    logger.warning(f"403错误 - 禁止访问: {request.url}")
    
    # 如果是AJAX请求，返回JSON响应
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return create_error_response(
            403,
            '禁止访问',
            '您没有权限访问此页面。',
            f"请求路径: {request.url}"
        )
    
    return render_template('errors/403.html'), 403

@main.app_errorhandler(400)
def bad_request(e):
    """处理400错误请求错误"""
    logger.warning(f"400错误 - 错误请求: {request.url}")
    
    # 如果是AJAX请求，返回JSON响应
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return create_error_response(
            400,
            '错误请求',
            '请求格式不正确，请检查请求参数。',
            f"请求路径: {request.url}"
        )
    
    return render_template('errors/400.html'), 400

@main.app_errorhandler(401)
def unauthorized(e):
    """处理401未授权错误"""
    logger.warning(f"401错误 - 未授权访问: {request.url}")
    
    # 如果是AJAX请求，返回JSON响应
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': '未授权',
            'message': '请先登录以访问此页面',
            'code': 401
        })
        response.status_code = 401
        return response
    
    # 对于普通请求，重定向到登录页面
    flash('请先登录以访问此页面', 'warning')
    return redirect(url_for('auth.login'))

@main.app_errorhandler(405)
def method_not_allowed(e):
    """处理405方法不允许错误"""
    logger.warning(f"405错误 - 方法不允许: {request.method} {request.url}")
    
    # 如果是AJAX请求，返回JSON响应
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return create_error_response(
            405,
            '方法不允许',
            f'{request.method} 方法不被允许。',
            f"请求路径: {request.url}"
        )
    
    return render_template('errors/405.html'), 405

@main.app_errorhandler(413)
def request_entity_too_large(e):
    """处理413请求实体过大错误"""
    logger.warning(f"413错误 - 请求实体过大: {request.url}")
    
    # 如果是AJAX请求，返回JSON响应
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return create_error_response(
            413,
            '请求实体过大',
            '上传的文件过大，请减小文件大小。',
            f"请求路径: {request.url}"
        )
    
    return render_template('errors/413.html'), 413

@main.app_errorhandler(429)
def too_many_requests(e):
    """处理429请求过多错误"""
    logger.warning(f"429错误 - 请求过多: {request.url}")
    
    # 如果是AJAX请求，返回JSON响应
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return create_error_response(
            429,
            '请求过多',
            '请求过于频繁，请稍后重试。',
            f"请求路径: {request.url}"
        )
    
    return render_template('errors/429.html'), 429

def handle_database_error(e):
    """处理数据库相关错误"""
    logger.error(f"数据库错误: {str(e)}")
    
    # 如果是AJAX请求，返回JSON响应
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': '数据库错误',
            'message': '数据库操作失败，请稍后重试',
            'code': 500
        })
        response.status_code = 500
        return response
    
    flash('数据库操作失败，请稍后重试', 'error')
    return redirect(url_for('main.index'))

def handle_validation_error(e):
    """处理数据验证错误"""
    logger.warning(f"数据验证错误: {str(e)}")
    
    # 如果是AJAX请求，返回JSON响应
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': '数据验证失败',
            'message': str(e),
            'code': 400
        })
        response.status_code = 400
        return response
    
    flash(f'数据验证失败: {str(e)}', 'warning')
    return redirect(request.referrer or url_for('main.index'))