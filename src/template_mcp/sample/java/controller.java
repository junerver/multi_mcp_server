package com.jkr.project.system.controller;

import java.util.List;

import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.jkr.framework.aspectj.lang.annotation.Log;
import com.jkr.framework.aspectj.lang.enums.BusinessType;
import com.jkr.project.system.domain.Prompt;
import com.jkr.project.system.service.IPromptService;
import com.jkr.framework.web.controller.BaseController;
import com.jkr.common.utils.poi.ExcelUtil;
import com.jkr.framework.web.domain.R;
import com.jkr.framework.web.page.TableDataInfo;

/**
 * AI提示词内容管理Controller
 *
 * @author jkr
 * @date 2025-09-01
 */
@RestController
@RequestMapping("/system/prompt")
public class PromptController extends BaseController {
    @Autowired
    private IPromptService promptService;

/**
 * 查询AI提示词内容管理列表
 */
@PreAuthorize("@ss.hasPermi('system:prompt:list')")
@GetMapping("/list")
    public R<TableDataInfo> list(Prompt prompt) {
        startPage();
        List<Prompt> list = promptService.selectPromptList(prompt);
        return getDataTable(list);
    }

    /**
     * 导出AI提示词内容管理列表
     */
    @PreAuthorize("@ss.hasPermi('system:prompt:export')")
    @Log(title = "导出AI提示词内容管理列表", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public R<Void> export(HttpServletResponse response, Prompt prompt) {
        List<Prompt> list = promptService.selectPromptList(prompt);
        ExcelUtil<Prompt> util = new ExcelUtil<Prompt>(Prompt. class);
        util.exportExcel(response, list, "AI提示词内容管理数据");
        return R.success();
    }

    /**
     * 获取AI提示词内容管理详细信息
     */
    @PreAuthorize("@ss.hasPermi('system:prompt:query')")
    @GetMapping(value = "/info/{id}")
    public R<prompt> getInfo(@PathVariable("id") Long id) {
        return R.success(promptService.selectPromptById(id));
    }

    /**
     * 新增AI提示词内容管理
     */
    @PreAuthorize("@ss.hasPermi('system:prompt:add')")
    @Log(title = "新增AI提示词内容管理", businessType = BusinessType.INSERT)
    @PostMapping(value = "/add")
    public R<Void> add(@Validated @RequestBody Prompt prompt) {
        return R.result(promptService.insertPrompt(prompt));
    }

    /**
     * 修改AI提示词内容管理
     */
    @PreAuthorize("@ss.hasPermi('system:prompt:edit')")
    @Log(title = "修改AI提示词内容管理", businessType = BusinessType.UPDATE)
    @PostMapping(value = "/edit")
    public R<Void> edit(@Validated @RequestBody Prompt prompt) {
        return R.result(promptService.updatePrompt(prompt));
    }

    /**
     * 删除AI提示词内容管理
     */
    @PreAuthorize("@ss.hasPermi('system:prompt:remove')")
    @Log(title = "删除AI提示词内容管理", businessType = BusinessType.DELETE)
    @PostMapping("/remove/{id}")
    public R<Void> remove(@PathVariable Long id) {
        return R.result(promptService.deletePromptById(id));
    }

    /**
     * 批量删除AI提示词内容管理
     */
    @PreAuthorize("@ss.hasPermi('system:prompt:batchRemove')")
    @Log(title = "批量删除AI提示词内容管理", businessType = BusinessType.DELETE)
    @PostMapping("/batchRemove")
    public R<Void> batchRemove(@RequestBody Prompt prompt) {
        return R.result(promptService.deletePromptByIds(prompt.getIds()));
    }
}
