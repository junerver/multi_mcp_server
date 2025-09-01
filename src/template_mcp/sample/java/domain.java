package com.jkr.project.system.domain;

import lombok.Data;
import lombok.EqualsAndHashCode;
import com.baomidou.mybatisplus.annotation.TableName;
import com.jkr.framework.aspectj.lang.annotation.Excel;
import com.jkr.framework.web.domain.BaseModel;
import java.util.List;

/**
 * AI提示词内容管理对象 ai_prompt
 *
 * @author jkr
 * @date 2025-09-01
 */
        @Data
        @EqualsAndHashCode(callSuper = true)
        @TableName("ai_prompt")
		public class Prompt extends BaseModel
		{
		private static final long serialVersionUID = 1L;

				/** 主键id */
		private Long id;

				/** prompt内容 */
				@Excel(name = "prompt内容")
		private String content;

				/** 是否启用 */
				@Excel(name = "是否启用")
		private Integer enabled;

				/** 创建者 */
		private String createBy;

				/** 创建时间 */
		private Date createTime;

				/** 更新者 */
		private String updateBy;

				/** 更新时间 */
		private Date updateTime;

				/** 删除标志（默认为1，表示数据可用，所有值为时间戳的表示数据不可用） */
		private String delFlag;

				/** 备注 */
				@Excel(name = "备注")
		private String remark;

            /** 主键集合 */
            private List<Long> ids;
}
