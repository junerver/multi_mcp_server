package com.jkr.project.system.mapper;

import java.util.List;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import com.jkr.project.system.domain.Prompt;

/**
 * AI提示词内容管理Mapper接口
 *
 * @author jkr
 * @date 2025-09-01
 */
@Mapper
public interface PromptMapper extends BaseMapper<Prompt>{
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
	 * 删除AI提示词内容管理
	 *
	 * @param id AI提示词内容管理主键
	 * @return 结果
	 */
	int deletePromptById(Long id);

	/**
	 * 批量删除AI提示词内容管理
	 *
	 * @param ids 需要删除的数据主键集合
	 * @return 结果
	 */
	int deletePromptByIds(Long[] ids);

	/**
	 * 批量逻辑删除AI提示词内容管理
	 *
	 * @param  ids AI提示词内容管理主键
	 * @return 结果
	 */
	int logicRemoveByIds(List<Long> ids);

	/**
	 * 通过AI提示词内容管理主键id逻辑删除信息
	 *
	 * @param  id AI提示词内容管理主键
	 * @return 结果
	 */
	int logicRemoveById(Long id);
}
