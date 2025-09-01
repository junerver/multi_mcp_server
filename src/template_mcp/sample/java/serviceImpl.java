package com.jkr.project.system.service.impl;

import java.util.List;
import com.jkr.common.utils.SecurityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.jkr.project.system.mapper.PromptMapper;
import com.jkr.project.system.domain.Prompt;
import com.jkr.project.system.service.IPromptService;
import org.springframework.transaction.annotation.Transactional;

/**
 * AI提示词内容管理Service业务层处理
 *
 * @author jkr
 * @date 2025-09-01
 */
@Service
@Transactional
public class PromptServiceImpl implements IPromptService {
	@Autowired
	private PromptMapper promptMapper;

	/**
	 * 查询AI提示词内容管理
	 *
	 * @param id AI提示词内容管理主键
	 * @return AI提示词内容管理
	 */
	@Override
	public Prompt selectPromptById(Long id) {
		return promptMapper.selectPromptById(id);
	}

	/**
	 * 查询AI提示词内容管理列表
	 *
	 * @param prompt AI提示词内容管理
	 * @return AI提示词内容管理
	 */
	@Override
	public List<Prompt> selectPromptList(Prompt prompt) {
		return promptMapper.selectPromptList(prompt);
	}

	/**
	 * 新增AI提示词内容管理
	 *
	 * @param prompt AI提示词内容管理
	 * @return 结果
	 */
	@Override
	@Transactional(readOnly = false, rollbackFor = Exception.class)
	public int insertPrompt(Prompt prompt) {
		prompt.insertInit(SecurityUtils.getLoginUser().getUsername());
        
			return promptMapper.insertPrompt(prompt);
	}

	/**
	 * 修改AI提示词内容管理
	 *
	 * @param prompt AI提示词内容管理
	 * @return 结果
	 */
	@Override
	@Transactional(readOnly = false, rollbackFor = Exception.class)
	public int updatePrompt(Prompt prompt) {
		prompt.updateInit(SecurityUtils.getLoginUser().getUsername());
        
		return promptMapper.updatePrompt(prompt);
	}

	/**
	 * 批量删除AI提示词内容管理
	 *
	 * @param ids 需要删除的AI提示词内容管理主键
	 * @return 结果
	 */
	@Override
	@Transactional(readOnly = false, rollbackFor = Exception.class)
	public int deletePromptByIds(List<Long> ids) {
		return promptMapper.logicRemoveByIds(ids);
		//return promptMapper.deletePromptByIds(ids);
	}

	/**
	 * 删除AI提示词内容管理信息
	 *
	 * @param id AI提示词内容管理主键
	 * @return 结果
	 */
	@Override
	@Transactional(readOnly = false, rollbackFor = Exception.class)
	public int deletePromptById(Long id) {
		return promptMapper.logicRemoveById(id);
		//return promptMapper.deletePromptById(id);
	}

}
