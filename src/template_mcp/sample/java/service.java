package com.jkr.project.system.service;

import java.util.List;

import com.jkr.project.system.domain .Prompt;

/**
 * AI提示词内容管理Service接口
 *
 * @author jkr
 * @date 2025-09-01
 */
public interface IPromptService {
	/**
	 * 查询AI提示词内容管理
	 *
	 * @param id AI提示词内容管理主键
	 * @return AI提示词内容管理
	 */
	Prompt selectPromptById(Long id);

	/**
	 * 查询AI提示词内容管理列表
	 *
	 * @param prompt AI提示词内容管理
	 * @return AI提示词内容管理集合
	 */
	List<Prompt> selectPromptList(Prompt prompt);

	/**
	 * 新增AI提示词内容管理
	 *
	 * @param prompt AI提示词内容管理
	 * @return 结果
	 */
	int insertPrompt(Prompt prompt);

	/**
	 * 修改AI提示词内容管理
	 *
	 * @param prompt AI提示词内容管理
	 * @return 结果
	 */
	int updatePrompt(Prompt prompt);

	/**
	 * 批量删除AI提示词内容管理
	 *
	 * @param ids 需要删除的AI提示词内容管理主键集合
	 * @return 结果
	 */
	int deletePromptByIds(List<Long> ids);

	/**
	 * 删除AI提示词内容管理信息
	 *
	 * @param id AI提示词内容管理主键
	 * @return 结果
	 */
	int deletePromptById(Long id);

}
