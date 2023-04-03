import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyFooterComponent } from './dairy-footer.component';

describe('DairyFooterComponent', () => {
  let component: DairyFooterComponent;
  let fixture: ComponentFixture<DairyFooterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyFooterComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyFooterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
